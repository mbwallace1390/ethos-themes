-- Royal Blue Strong
-- Standalone ETHOS cancer-awareness radio theme.
-- Rotorflight and RF Suite files are not modified.
local function init()
    system.registerTheme({
        key = "RoyBlue",
        name = "Royal Blue Strong",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x1A, 0x31, 0x56), -- SECONDARY_BGCOLOR
            lcd.RGB(0x27, 0x5D, 0xCE), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x71, 0x82), -- DISABLE_COLOR
            lcd.RGB(0x11, 0x1F, 0x38), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x98, 0xB2, 0xE6), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x08, 0x0E, 0x1A), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xA9, 0xC8, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x75, 0x7E, 0x8D), -- INACTIVE_COLOR
            lcd.RGB(0xA9, 0xC8, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x31, 0x54, 0x8A), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x08, 0x0E, 0x1A), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-royal-blue-strong.png"),
    })
end

return { init = init }
