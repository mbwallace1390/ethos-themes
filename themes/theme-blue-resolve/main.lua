-- Blue Resolve
-- Standalone ETHOS cancer-awareness radio theme.
-- Rotorflight and RF Suite files are not modified.
local function init()
    system.registerTheme({
        key = "BluRsv",
        name = "Blue Resolve",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x1D, 0x3E, 0x56), -- SECONDARY_BGCOLOR
            lcd.RGB(0x7E, 0xC8, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0A, 0x0D), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x69, 0x77, 0x84), -- DISABLE_COLOR
            lcd.RGB(0x13, 0x29, 0x3B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xBF, 0xE2, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x09, 0x13, 0x1C), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xD3, 0xEE, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x76, 0x84, 0x8F), -- INACTIVE_COLOR
            lcd.RGB(0xD3, 0xEE, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x35, 0x66, 0x85), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x09, 0x13, 0x1C), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-blue-resolve.png"),
    })
end

return { init = init }
