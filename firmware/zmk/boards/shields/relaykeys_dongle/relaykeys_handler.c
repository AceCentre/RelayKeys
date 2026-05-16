#include <zephyr/kernel.h>
#include <zmk/endpoints.h>
#include <zmk/hid.h>
#include <pb_decode.h>
#include <zmk/rpc/rpc.h>

// Simple protobuf definition generated structurally for Nanopb
// This avoids needing nanopb compilation inside Zephyr for a single struct test
typedef struct _relaykeys_rpc_InjectReportRequest {
    int32_t type;
    pb_callback_t data;
} relaykeys_rpc_InjectReportRequest;

#define relaykeys_rpc_InjectReportRequest_fields \
    PB_FIELD(  1, INT32   , SINGULAR, STATIC  , FIRST, relaykeys_rpc_InjectReportRequest, type, type, 0), \
    PB_FIELD(  2, BYTES   , SINGULAR, CALLBACK, OTHER, relaykeys_rpc_InjectReportRequest, data, type, 0), \
    PB_LAST_FIELD

static bool decode_data_callback(pb_istream_t *stream, const pb_field_t *field, void **arg)
{
    // Our HID report buffer
    uint8_t report_data[16] = {0};
    size_t len = stream->bytes_left;
    if (len > sizeof(report_data)) return false;

    if (!pb_read(stream, report_data, len))
        return false;

    // Send Keyboard report
    struct zmk_hid_keyboard_report_body report;
    memset(&report, 0, sizeof(report));
    if (len > 0) report.modifiers = report_data[0];
    for (size_t i = 2; i < len && i - 2 < 6; i++) {
        report.keys[i-2] = report_data[i];
    }

    // Inject report
    zmk_hid_keyboard_report_set(&report);
    zmk_endpoints_send_report(ZMK_ENDPOINT_BLE);

    return true;
}

// Handler for the RPC request
static int handle_inject_report(const pb_msgdesc_t *req_desc, pb_istream_t *req_stream,
                                const pb_msgdesc_t *resp_desc, pb_ostream_t *resp_stream) {

    relaykeys_rpc_InjectReportRequest req = {0};
    req.data.funcs.decode = decode_data_callback;

    if (!pb_decode(req_stream, relaykeys_rpc_InjectReportRequest_fields, &req)) {
        return -EINVAL;
    }

    return 0;
}

ZMK_RPC_SUBSYSTEM(relaykeys_inject,
    ZMK_RPC_HANDLER(0, handle_inject_report)
);
