#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/sys/reboot.h>
#include <zephyr/logging/log.h>
#include <string.h>

#include <zmk/hid.h>
#include <zmk/endpoints.h>
#include <zmk/ble.h>

#include <dt-bindings/zmk/hid_usage_pages.h>

LOG_MODULE_REGISTER(relaykeys, LOG_LEVEL_INF);

#define SOF_BYTE 0xAB
#define ESC_BYTE 0xAC
#define EOF_BYTE 0xAD

#define MAX_FRAME 128
#define RING_SIZE 512

static const struct device *uart_dev;
static uint8_t ring_buf[RING_SIZE];
static volatile size_t ring_head;
static volatile size_t ring_tail;
static uint8_t frame_buf[MAX_FRAME];
static size_t frame_len;
static bool in_frame;
static bool esc_next;

K_MUTEX_DEFINE(tx_mutex);

static void uart_isr(const struct device *dev, void *ctx) {
    while (uart_irq_update(dev) && uart_irq_is_pending(dev)) {
        if (!uart_irq_rx_ready(dev)) {
            break;
        }
        uint8_t tmp[64];
        int n = uart_fifo_read(dev, tmp, sizeof(tmp));
        for (int i = 0; i < n; i++) {
            size_t next = (ring_head + 1) % RING_SIZE;
            if (next != ring_tail) {
                ring_buf[ring_head] = tmp[i];
                ring_head = next;
            }
        }
    }
}

static int read_varint(const uint8_t *buf, size_t len, uint32_t *val) {
    *val = 0;
    int i = 0;
    while (i < 5 && (size_t)i < len) {
        *val |= (uint32_t)(buf[i] & 0x7F) << (7 * i);
        if (!(buf[i] & 0x80)) {
            return i + 1;
        }
        i++;
    }
    return -1;
}

static bool decode_report(const uint8_t *data, size_t len, int32_t *type,
                          uint8_t *payload, size_t *payload_len) {
    size_t pos = 0;
    *type = 0;
    *payload_len = 0;

    while (pos < len) {
        uint32_t tag;
        int n = read_varint(data + pos, len - pos, &tag);
        if (n <= 0) return false;
        pos += n;
        int field = tag >> 3;
        int wt = tag & 7;

        if (field == 1 && wt == 0) {
            uint32_t v;
            n = read_varint(data + pos, len - pos, &v);
            if (n <= 0) return false;
            *type = (int32_t)v;
            pos += n;
        } else if (field == 2 && wt == 2) {
            uint32_t dlen;
            n = read_varint(data + pos, len - pos, &dlen);
            if (n <= 0) return false;
            pos += n;
            if (pos + dlen > len || dlen > 16) return false;
            memcpy(payload, data + pos, dlen);
            *payload_len = dlen;
            pos += dlen;
        } else {
            if (wt == 0) {
                uint32_t v;
                n = read_varint(data + pos, len - pos, &v);
                if (n <= 0) return false;
                pos += n;
            } else if (wt == 2) {
                uint32_t l;
                n = read_varint(data + pos, len - pos, &l);
                if (n <= 0) return false;
                pos += n + l;
            } else {
                return false;
            }
        }
    }
    return true;
}

static bool decode_admin(const uint8_t *data, size_t len, int32_t *cmd, int32_t *slot) {
    size_t pos = 0;
    *cmd = 0;
    *slot = 0;

    while (pos < len) {
        uint32_t tag;
        int n = read_varint(data + pos, len - pos, &tag);
        if (n <= 0) return false;
        pos += n;
        int field = tag >> 3;
        int wt = tag & 7;

        if (wt == 0) {
            uint32_t v;
            n = read_varint(data + pos, len - pos, &v);
            if (n <= 0) return false;
            if (field == 1) *cmd = (int32_t)v;
            else if (field == 2) *slot = (int32_t)v;
            pos += n;
        } else if (wt == 2) {
            uint32_t l;
            n = read_varint(data + pos, len - pos, &l);
            if (n <= 0) return false;
            pos += n + l;
        }
    }
    return true;
}

static size_t encode_varint(uint8_t *buf, uint32_t val) {
    size_t i = 0;
    while (val >= 0x80) {
        buf[i++] = (val & 0x7F) | 0x80;
        val >>= 7;
    }
    buf[i++] = val & 0x7F;
    return i;
}

static size_t encode_admin_response(bool success, int32_t active_slot, uint8_t *buf, size_t max) {
    size_t pos = 0;
    buf[pos++] = 0x08;
    buf[pos++] = success ? 0x01 : 0x00;
    if (active_slot >= 0) {
        buf[pos++] = 0x18;
        pos += encode_varint(buf + pos, (uint32_t)active_slot);
    }
    return pos;
}

static void send_framed(const uint8_t *data, size_t len) {
    k_mutex_lock(&tx_mutex, K_FOREVER);
    uart_poll_out(uart_dev, SOF_BYTE);
    for (size_t i = 0; i < len; i++) {
        if (data[i] == SOF_BYTE || data[i] == ESC_BYTE || data[i] == EOF_BYTE) {
            uart_poll_out(uart_dev, ESC_BYTE);
        }
        uart_poll_out(uart_dev, data[i]);
    }
    uart_poll_out(uart_dev, EOF_BYTE);
    k_mutex_unlock(&tx_mutex);
}

static void handle_inject_report(int32_t type, const uint8_t *data, size_t data_len) {
    if (type == 0) {
        struct zmk_hid_keyboard_report *rpt = zmk_hid_get_keyboard_report();
        if (data_len > 0) {
            rpt->body.modifiers = data[0];
        }
        for (int i = 0; i < CONFIG_ZMK_HID_KEYBOARD_REPORT_SIZE; i++) {
            rpt->body.keys[i] = ((size_t)(i + 2) < data_len) ? data[i + 2] : 0;
        }
        zmk_endpoint_send_report(HID_USAGE_KEY);
    } else if (type == 1) {
#if IS_ENABLED(CONFIG_ZMK_POINTING)
        struct zmk_hid_mouse_report *rpt = zmk_hid_get_mouse_report();
        if (data_len >= 1) rpt->body.buttons = data[0];
        rpt->body.d_x = (data_len >= 3) ? (int16_t)(int8_t)data[1] : 0;
        rpt->body.d_y = (data_len >= 3) ? (int16_t)(int8_t)data[2] : 0;
        rpt->body.d_scroll_y = (data_len >= 5) ? (int16_t)(int8_t)data[3] : 0;
        rpt->body.d_scroll_x = (data_len >= 5) ? (int16_t)(int8_t)data[4] : 0;
        zmk_endpoint_send_mouse_report();
#endif
    } else if (type == 2) {
        struct zmk_hid_consumer_report *rpt = zmk_hid_get_consumer_report();
        if (data_len >= 2) {
            uint16_t usage = data[0] | ((uint16_t)data[1] << 8);
            rpt->body.keys[0] = usage;
            for (int i = 1; i < CONFIG_ZMK_HID_CONSUMER_REPORT_SIZE; i++) {
                rpt->body.keys[i] = 0;
            }
        }
        zmk_endpoint_send_report(HID_USAGE_CONSUMER);
    }
}

static void handle_admin_command(int32_t cmd, int32_t slot) {
    uint8_t resp[32];
    size_t resp_len;

    switch (cmd) {
    case 0:
        zmk_ble_clear_bonds();
        break;
    case 1:
        if (slot >= 0 && slot < 5) {
            zmk_ble_prof_select((uint8_t)slot);
        }
        break;
    case 2:
        break;
    case 3:
        resp_len = encode_admin_response(true, -1, resp, sizeof(resp));
        send_framed(resp, resp_len);
        k_sleep(K_MSEC(100));
        sys_reboot(SYS_REBOOT_WARM);
        return;
    case 4:
        if (slot >= 0 && slot < 5) {
            int current = zmk_ble_active_profile_index();
            zmk_ble_prof_select((uint8_t)slot);
            zmk_ble_clear_bonds();
            zmk_ble_prof_select((uint8_t)current);
        }
        break;
    }

    int32_t active = zmk_ble_active_profile_index();
    resp_len = encode_admin_response(true, active, resp, sizeof(resp));
    send_framed(resp, resp_len);
}

static void process_frame(const uint8_t *data, size_t len) {
    if (len < 2) return;

    uint32_t tag;
    int n = read_varint(data, len, &tag);
    if (n <= 0) return;
    int field = tag >> 3;
    int wt = tag & 7;

    if (field != 1 || wt != 0) return;

    uint32_t type_val;
    int n2 = read_varint(data + n, len - n, &type_val);
    if (n2 <= 0) return;
    size_t pos = (size_t)(n + n2);
    if (pos >= len) return;

    uint32_t tag2;
    int n3 = read_varint(data + pos, len - pos, &tag2);
    if (n3 <= 0) return;
    int wt2 = tag2 & 7;

    if (wt2 == 2) {
        int32_t type;
        uint8_t payload[16];
        size_t payload_len;
        if (decode_report(data, len, &type, payload, &payload_len)) {
            handle_inject_report(type, payload, payload_len);
        }
    } else if (wt2 == 0) {
        int32_t cmd, slot;
        if (decode_admin(data, len, &cmd, &slot)) {
            handle_admin_command(cmd, slot);
        }
    }
}

static void relaykeys_thread(void) {
    uart_dev = DEVICE_DT_GET(DT_CHOSEN(relaykeys_uart));
    if (!device_is_ready(uart_dev)) {
        LOG_ERR("RelayKeys UART not ready");
        return;
    }

    LOG_INF("RelayKeys UART ready, waiting for USB...");
    k_sleep(K_SECONDS(3));

    uart_irq_callback_set(uart_dev, uart_isr);
    uart_irq_rx_enable(uart_dev);

    LOG_INF("RelayKeys listening");
    in_frame = false;
    esc_next = false;
    frame_len = 0;

    for (;;) {
        if (ring_tail == ring_head) {
            k_sleep(K_MSEC(1));
            continue;
        }

        uint8_t b = ring_buf[ring_tail];
        ring_tail = (ring_tail + 1) % RING_SIZE;

        if (esc_next) {
            esc_next = false;
            if (in_frame && frame_len < MAX_FRAME) {
                frame_buf[frame_len++] = b;
            }
            continue;
        }

        if (b == SOF_BYTE) {
            in_frame = true;
            frame_len = 0;
        } else if (b == EOF_BYTE && in_frame) {
            if (frame_len > 0) {
                process_frame(frame_buf, frame_len);
            }
            in_frame = false;
            frame_len = 0;
        } else if (b == ESC_BYTE && in_frame) {
            esc_next = true;
        } else if (in_frame && frame_len < MAX_FRAME) {
            frame_buf[frame_len++] = b;
        }
    }
}

K_THREAD_DEFINE(relaykeys_tid, 1024, relaykeys_thread, NULL, NULL, NULL,
                K_LOWEST_APPLICATION_THREAD_PRIO, 0, 0);
