-- Orange Warrior
-- Standalone ETHOS cancer-awareness radio theme.
-- Rotorflight and RF Suite files are not modified.
local function init()
    system.registerTheme({
        key = "OrgWar",
        name = "Orange Warrior",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x51, 0x2B, 0x10), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x8A, 0x2A), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0A, 0x0D), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x7E, 0x6F, 0x65), -- DISABLE_COLOR
            lcd.RGB(0x35, 0x1C, 0x0A), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xFA, 0xC6, 0x9C), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x1A, 0x0E, 0x05), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xD2, 0xA8), -- ACTIVE_COLOR
            lcd.RGB(0x89, 0x7C, 0x74), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0xD2, 0xA8), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x84, 0x49, 0x1C), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x1A, 0x0E, 0x05), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-orange-warrior.png"),
    })
end

return { init = init }
