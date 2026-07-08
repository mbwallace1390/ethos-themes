-- RF Emerald Pro
-- Lightweight RF Pro outline-focus color variant.
local function init()
    system.registerTheme({
        key = "RFEmer",
        name = "RF Emerald Pro",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            lcd.RGB(0x16, 0x30, 0x2B), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0xD6, 0x8F), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x0D, 0x1D, 0x1A), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x07, 0x11, 0x0F), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            lcd.RGB(0x00, 0xD6, 0x8F), -- ACTIVE_COLOR
            lcd.RGB(0x68, 0x97, 0x89), -- INACTIVE_COLOR
            lcd.RGB(0x00, 0xD6, 0x8F), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x2C, 0x56, 0x4A), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x07, 0x11, 0x0F), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarBackground = lcd.loadBitmap("toolbar-rf-emerald-pro.png"),
    })
end

return {
    init = init
}
