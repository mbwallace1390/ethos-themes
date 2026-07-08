-- Pink Hope
-- Standalone ETHOS cancer-awareness radio theme.
-- Rotorflight and RF Suite files are not modified.
local function init()
    system.registerTheme({
        key = "PinkHp",
        name = "Pink Hope",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x4A, 0x25, 0x35), -- SECONDARY_BGCOLOR
            lcd.RGB(0xF4, 0x8F, 0xB1), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0A, 0x0D), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x7C, 0x6D, 0x75), -- DISABLE_COLOR
            lcd.RGB(0x32, 0x18, 0x24), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xF5, 0xC8, 0xD9), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x1A, 0x0E, 0x15), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xD1, 0xE1), -- ACTIVE_COLOR
            lcd.RGB(0x88, 0x7A, 0x82), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0xD1, 0xE1), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x7B, 0x40, 0x58), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x1A, 0x0E, 0x15), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-pink-hope.png"),
    })
end

return { init = init }
