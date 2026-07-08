-- RF Gold Pro
-- Lightweight RF Pro outline-focus color variant.
local function init()
    system.registerTheme({
        key = "RFGold",
        name = "RF Gold Pro",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            lcd.RGB(0x35, 0x2D, 0x14), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0xC4, 0x00), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x21, 0x1B, 0x09), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x13, 0x0F, 0x04), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xC4, 0x00), -- ACTIVE_COLOR
            lcd.RGB(0xA5, 0x95, 0x65), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0xC4, 0x00), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x62, 0x52, 0x22), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x13, 0x0F, 0x04), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarBackground = lcd.loadBitmap("toolbar-rf-gold-pro.png"),
    })
end

return {
    init = init
}
