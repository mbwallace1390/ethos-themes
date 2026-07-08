-- Daylight Blue
-- Lightweight standalone ETHOS theme.
local function init()
    system.registerTheme({
        key = "DayBlu",
        name = "Daylight Blue",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0x12, 0x18, 0x1E), -- PRIMARY_COLOR
            lcd.RGB(0xD5, 0xE1, 0xED), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0x6E, 0xDC), -- HIGHLIGHT_COLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x91, 0x99, 0xA1), -- DISABLE_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x2F, 0x46, 0x5C), -- SECONDARY_COLOR
            lcd.RGB(0x14, 0x91, 0x50), -- SAFE_COLOR
            lcd.RGB(0xEC, 0xF2, 0xF9), -- PAGE_BGCOLOR
            lcd.RGB(0xCC, 0x28, 0x32), -- ERROR_COLOR
            lcd.RGB(0x00, 0x6E, 0xDC), -- ACTIVE_COLOR
            lcd.RGB(0x69, 0x77, 0x84), -- INACTIVE_COLOR
            lcd.RGB(0x00, 0x6E, 0xDC), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0xB1, 0xBD, 0xC9), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xBE, 0x73, 0x00), -- WARNING_COLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0xEC, 0xF2, 0xF9), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-daylight-blue.png"),
    })
end

return { init = init }
