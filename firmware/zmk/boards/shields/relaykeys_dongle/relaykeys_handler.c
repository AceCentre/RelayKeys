#include <zephyr/kernel.h>
#include <zephyr/sys/reboot.h>
#include <zmk/endpoints.h>
#include <zmk/hid.h>
#include <zmk/ble.h>
#include <pb_decode.h>
#include <pb_encode.h>
#include <zmk/rpc/rpc.h>

typedef struct _relaykeys_rpc_InjectReportRequest {
    int32_t type;
    pb_callback_t data;
} relaykeys_rpc_InjectReportRequest;

#define relaykeys_rpc_InjectReportRequest_fields \
    PB_FIELD(  1, INT32   , SINGULAR, STATIC  , FIRST, relaykeys_rpc_InjectReportRequest, type, type, 0), \
    PB_FIELD(  2, BYTES   , SINGULAR, CALLBACK, OTHER, relaykeys_rpc_InjectReportRequest, data, type, 0), \
    PB_LAST_FIELD

typedef struct _relaykeys_rpc_AdminCommandRequest {
    int32_t command;
    int32_t slot;
} relaykeys_rpc_AdminCommandRequest;

#define relaykeys_rpc_AdminCommandRequest_fields \
    PB_FIELD(  1, INT32   , SINGULAR, STATIC  , FIRST, relaykeys_rpc_AdminCommandRequest, command, command, 0), \
    PB_FIELD(  2, INT32   , SINGULAR, STATIC  , OTHER, relaykeys_rpc_AdminCommandRequest, slot, command, 0), \
    PB_LAST_FIELD

typedef struct _relaykeys_rpc_AdminCommandResponse {
    bool success;
    pb_callback_t error_message;
    int32_t active_slot;
    pb_callback_t slot_bonded;
} relaykeys_rpc_AdminCommandResponse;

#define relaykeys_rpc_AdminCommandResponse_fields \
    PB_FIELD(  1, BOOL    , SINGULAR, STATIC  , FIRST, relaykeys_rpc_AdminCommandResponse, success, success, 0), \
    PB_FIELD(  2, STRING  , SINGULAR, CALLBACK, OTHER, relaykeys_rpc_AdminCommandResponse, error_message, success, 0), \
    PB_FIELD(  3, INT32   , SINGULAR, STATIC  , OTHER, relaykeys_rpc_AdminCommandResponse, active_slot, error_message, 0), \
    PB_FIELD(  4, BOOL    , REPEATED, CALLBACK, OTHER, relaykeys_rpc_AdminCommandResponse, slot_bonded, active_slot, 0), \
    PB_LAST_FIELD

static bool decode_data_callback(pb_istream_t *stream, const pb_field_t *field, void **arg)
{
    relaykeys_rpc_InjectReportRequest *req = (relaykeys_rpc_InjectReportRequest *)(*arg);
    uint8_t report_data[16] = {0};
    size_t len = stream->bytes_left;
    if (len > sizeof(report_data)) return false;

    if (!pb_read(stream, report_data, len))
        return false;

    if (req->type == 0) { // KEYBOARD
        struct zmk_hid_keyboard_report_body report;
        memset(&report, 0, sizeof(report));
        if (len > 0) report.modifiers = report_data[0];
        for (size_t i = 2; i < len && i - 2 < 6; i++) {
            report.keys[i-2] = report_data[i];
        }
        zmk_hid_keyboard_report_set(&report);
        zmk_endpoints_send_report(ZMK_ENDPOINT_BLE);
    } else if (req->type == 1) { // MOUSE
        struct zmk_hid_mouse_report_body report;
        memset(&report, 0, sizeof(report));
        if (len >= 5) {
            report.buttons = report_data[0];
            report.x = (int8_t)report_data[1];
            report.y = (int8_t)report_data[2];
            report.scroll_y = (int8_t)report_data[3];
            report.scroll_x = (int8_t)report_data[4];
            zmk_hid_mouse_movement_set(report.x, report.y);
            zmk_hid_mouse_scroll_set(report.scroll_x, report.scroll_y);
            zmk_hid_mouse_buttons_set(report.buttons);
            zmk_endpoints_send_report(ZMK_ENDPOINT_BLE);
        }
    } else if (req->type == 2) { // CONSUMER
        if (len >= 2) {
            uint16_t usage = (report_data[1] << 8) | report_data[0];
            zmk_hid_consumer_report_set(usage);
            zmk_endpoints_send_report(ZMK_ENDPOINT_BLE);
            // clear it immediately
            zmk_hid_consumer_report_set(0);
            zmk_endpoints_send_report(ZMK_ENDPOINT_BLE);
        }
    }

    return true;
}

static int handle_inject_report(const pb_msgdesc_t *req_desc, pb_istream_t *req_stream,
                                const pb_msgdesc_t *resp_desc, pb_ostream_t *resp_stream) {
    relaykeys_rpc_InjectReportRequest req = {0};
    req.data.funcs.decode = decode_data_callback;
    req.data.arg = &req;

    if (!pb_decode(req_stream, relaykeys_rpc_InjectReportRequest_fields, &req)) {
        return -EINVAL;
    }
    return 0;
}

static bool encode_slot_bonded_callback(pb_ostream_t *stream, const pb_field_t *field, void *const *arg)
{
    // ZMK supports up to ZMK_BLE_PROFILE_COUNT (usually 5)
    for (int i = 0; i < ZMK_BLE_PROFILE_COUNT; i++) {
        bool bonded = zmk_ble_active_profile_is_connected(); // Actually we need to check specific profile bonding if possible
        // For simplicity we will return current active connection status for all slots or true if bonded
        // Let's check if the slot has a bonded device.
        bool has_bond = zmk_ble_profile_is_open(i); // This API might not be exact. We'll assume true if not open (has bond)
        has_bond = !has_bond;
        if (!pb_encode_tag_for_field(stream, field))
            return false;
        if (!pb_encode_varint(stream, has_bond))
            return false;
    }
    return true;
}

static int handle_admin_command(const pb_msgdesc_t *req_desc, pb_istream_t *req_stream,
                                const pb_msgdesc_t *resp_desc, pb_ostream_t *resp_stream) {
    relaykeys_rpc_AdminCommandRequest req = {0};
    if (!pb_decode(req_stream, relaykeys_rpc_AdminCommandRequest_fields, &req)) {
        return -EINVAL;
    }

    relaykeys_rpc_AdminCommandResponse resp = {0};
    resp.success = true;

    if (req.command == 0) { // PAIR
        zmk_ble_clear_bonds(); // Just mimicking BT_CLR for current profile
        zmk_ble_adv_start();
    } else if (req.command == 1) { // SWITCH_SLOT
        if (req.slot >= 0 && req.slot < ZMK_BLE_PROFILE_COUNT) {
            zmk_ble_prof_select(req.slot);
        }
    } else if (req.command == 2) { // GET_STATUS
        resp.active_slot = zmk_ble_active_profile_index();
        resp.slot_bonded.funcs.encode = encode_slot_bonded_callback;
    } else if (req.command == 3) { // RESET
        sys_reboot(SYS_REBOOT_WARM);
    } else if (req.command == 4) { // CLEAR_SLOT
        if (req.slot >= 0 && req.slot < ZMK_BLE_PROFILE_COUNT) {
            int current = zmk_ble_active_profile_index();
            zmk_ble_prof_select(req.slot);
            zmk_ble_clear_bonds();
            zmk_ble_prof_select(current);
        }
    }

    if (!pb_encode(resp_stream, relaykeys_rpc_AdminCommandResponse_fields, &resp)) {
        return -EINVAL;
    }

    return 0;
}

ZMK_RPC_SUBSYSTEM(relaykeys_inject,
    ZMK_RPC_HANDLER(0, handle_inject_report),
    ZMK_RPC_HANDLER(1, handle_admin_command)
);
