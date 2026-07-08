-- RF Magenta Pro
-- Lightweight RF Pro outline-focus color variant.
local function init()
    system.registerTheme({
        key = "RFMagn",
        name = "RF Magenta Pro",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            lcd.RGB(0x36, 0x19, 0x2B), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x3E, 0xA4), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x22, 0x0D, 0x1A), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x14, 0x07, 0x0F), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x3E, 0xA4), -- ACTIVE_COLOR
            lcd.RGB(0xAC, 0x70, 0x92), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0x3E, 0xA4), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x67, 0x31, 0x4F), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x14, 0x07, 0x0F), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarBackground = lcd.loadBitmap("toolbar-rf-magenta-pro.png"),
    })
end

return {
    init = init
}
