-- RF Crimson Pro
-- Lightweight RF Pro outline-focus color variant.
local function init()
    system.registerTheme({
        key = "RFCrim",
        name = "RF Crimson Pro",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            lcd.RGB(0x36, 0x19, 0x20), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x33, 0x4F), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x22, 0x0D, 0x12), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x14, 0x07, 0x0A), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x33, 0x4F), -- ACTIVE_COLOR
            lcd.RGB(0xA6, 0x6D, 0x77), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0x33, 0x4F), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x65, 0x2F, 0x3A), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x14, 0x07, 0x0A), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarBackground = lcd.loadBitmap("toolbar-rf-crimson-pro.png"),
    })
end

return {
    init = init
}
