-- RF Ember Pro
-- Lightweight RF Pro outline-focus color variant.
local function init()
    system.registerTheme({
        key = "RFEmbr",
        name = "RF Ember Pro",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            lcd.RGB(0x35, 0x20, 0x14), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x6A, 0x00), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x22, 0x12, 0x0A), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x14, 0x0A, 0x05), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x6A, 0x00), -- ACTIVE_COLOR
            lcd.RGB(0xA6, 0x7F, 0x66), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0x6A, 0x00), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x63, 0x3C, 0x22), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x14, 0x0A, 0x05), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarBackground = lcd.loadBitmap("toolbar-rf-ember-pro.png"),
    })
end

return {
    init = init
}
