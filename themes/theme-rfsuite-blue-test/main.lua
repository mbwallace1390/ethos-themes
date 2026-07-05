-- RF Suite Blue Test theme for ETHOS 26.1+
-- Purpose: verify that standard ETHOS focus/highlight colors control
-- the selected menu tiles inside Rotorflight RF Suite.

local function init()
    system.registerTheme({
        key = "RFBlueTest",
        name = "RF Suite Blue Test",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF2, 0xF4, 0xF8), -- PRIMARY_COLOR
            lcd.RGB(0x31, 0x36, 0x40), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0x6F, 0xE6), -- HIGHLIGHT_COLOR: selected/focused background
            COLOR_WHITE,               -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x74, 0x7A, 0x84), -- DISABLE_COLOR
            lcd.RGB(0x20, 0x24, 0x2B), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xC8, 0xCF, 0xD9), -- SECONDARY_COLOR
            lcd.RGB(0x84, 0xC3, 0x0F), -- SAFE_COLOR
            lcd.RGB(0x16, 0x19, 0x1F), -- PAGE_BGCOLOR
            lcd.RGB(0xF0, 0x4B, 0x4B), -- ERROR_COLOR
            lcd.RGB(0x00, 0x6F, 0xE6), -- ACTIVE_COLOR
            lcd.RGB(0x4B, 0x55, 0x63), -- INACTIVE_COLOR
            lcd.RGB(0x00, 0x6F, 0xE6), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x5A, 0x63, 0x70), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xA5, 0x00), -- WARNING_COLOR
            COLOR_BLACK,               -- SAFE_CONTRASTING_COLOR
            COLOR_BLACK,               -- TOPLCD_BGCOLOR
        }
    })
end

return {
    init = init
}
