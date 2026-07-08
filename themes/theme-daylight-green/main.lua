-- Daylight Green
-- Lightweight standalone ETHOS theme.
local function init()
    system.registerTheme({
        key = "DayGrn",
        name = "Daylight Green",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0x12, 0x18, 0x1E), -- PRIMARY_COLOR
            lcd.RGB(0xD7, 0xE3, 0xE1), -- SECONDARY_BGCOLOR
            lcd.RGB(0x13, 0x8A, 0x4B), -- HIGHLIGHT_COLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x91, 0x99, 0xA1), -- DISABLE_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x31, 0x48, 0x4E), -- SECONDARY_COLOR
            lcd.RGB(0x14, 0x91, 0x50), -- SAFE_COLOR
            lcd.RGB(0xED, 0xF3, 0xF4), -- PAGE_BGCOLOR
            lcd.RGB(0xCC, 0x28, 0x32), -- ERROR_COLOR
            lcd.RGB(0x13, 0x8A, 0x4B), -- ACTIVE_COLOR
            lcd.RGB(0x69, 0x77, 0x84), -- INACTIVE_COLOR
            lcd.RGB(0x13, 0x8A, 0x4B), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0xB2, 0xBF, 0xC0), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xBE, 0x73, 0x00), -- WARNING_COLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0xED, 0xF3, 0xF4), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-daylight-green.png"),
    })
end

return { init = init }
