-- RF Suite Blue theme for ETHOS 26.1+
-- Changes the ETHOS focus/highlight color from yellowish to blue.

local function init()
    system.registerTheme({
        key = "RFSuiteBlue",
        name = "RF Suite Blue",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF8, 0xF8, 0xF2), -- PRIMARY_COLOR
            lcd.RGB(0x31, 0x36, 0x40), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0x78, 0xE8), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x74, 0x7A, 0x84), -- DISABLE_COLOR
            lcd.RGB(0x20, 0x24, 0x2B), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xC8, 0xCF, 0xD9), -- SECONDARY_COLOR
            lcd.RGB(0x69, 0xFF, 0x94), -- SAFE_COLOR
            lcd.RGB(0x16, 0x19, 0x1F), -- PAGE_BGCOLOR
            lcd.RGB(0xDE, 0x57, 0x35), -- ERROR_COLOR
            lcd.RGB(0x00, 0x78, 0xE8), -- ACTIVE_COLOR
            lcd.RGB(0xA8, 0xB0, 0xBC), -- INACTIVE_COLOR
            lcd.RGB(0x00, 0x78, 0xE8), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x50, 0x52, 0x61), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xA5, 0x00), -- WARNING_COLOR
            lcd.RGB(0x16, 0x19, 0x1F), -- SAFE_CONTRASTING_COLOR
            COLOR_BLACK,               -- TOPLCD_BGCOLOR (XE/S)
        },
    })
end

return {
    init = init
}
