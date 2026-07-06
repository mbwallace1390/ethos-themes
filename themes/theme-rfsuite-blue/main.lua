-- @author flyingeek
-- Based on the known-working Dracula ETHOS theme package.
-- Selection-related colors changed to blue for Rotorflight RF Suite testing.
--
local function init()
    system.registerTheme({
        key = "RFSuiteBlue",
        name = "RF Suite Blue",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF8, 0xF8, 0xF2), -- PRIMARY_COLOR
            lcd.RGB(0x42, 0x44, 0x50), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0x78, 0xE8), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x62, 0x72, 0xA4), -- DISABLE_COLOR
            lcd.RGB(0x21, 0x22, 0x2C), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB8, 0xC3, 0xE4), -- SECONDARY_COLOR
            lcd.RGB(0x69, 0xFF, 0x94), -- SAFE_COLOR
            lcd.RGB(0x19, 0x1A, 0x21), -- PAGE_BGCOLOR
            lcd.RGB(0xDE, 0x57, 0x35), -- ERROR_COLOR
            lcd.RGB(0x00, 0x78, 0xE8), -- ACTIVE_COLOR
            lcd.RGB(0xB8, 0xC3, 0xE4), -- INACTIVE_COLOR
            lcd.RGB(0x00, 0x78, 0xE8), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x50, 0x52, 0x61), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xA3, 0x95, 0x14), -- WARNING_COLOR
            lcd.RGB(0x19, 0x1A, 0x21), -- SAFE_CONTRASTING_COLOR
            COLOR_BLACK,               -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarBackground = lcd.loadBitmap("toolbar-rfsuite-blue.png"),
    })
end
return {
    init = init
}
