-- Titanium
-- Lightweight standalone ETHOS theme.
local function init()
    system.registerTheme({
        key = "Titani",
        name = "Titanium",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x41, 0x48, 0x4F), -- SECONDARY_BGCOLOR
            lcd.RGB(0xC8, 0xD2, 0xDC), -- HIGHLIGHT_COLOR
            lcd.RGB(0x12, 0x16, 0x1A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x74, 0x79, 0x7E), -- DISABLE_COLOR
            lcd.RGB(0x2F, 0x35, 0x3B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xE0, 0xE6, 0xEC), -- SECONDARY_COLOR
            lcd.RGB(0x3F, 0xEB, 0x7F), -- SAFE_COLOR
            lcd.RGB(0x1F, 0x24, 0x29), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x44, 0x4D), -- ERROR_COLOR
            lcd.RGB(0xC8, 0xD2, 0xDC), -- ACTIVE_COLOR
            lcd.RGB(0x84, 0x88, 0x8D), -- INACTIVE_COLOR
            lcd.RGB(0xCC, 0xD6, 0xDF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x5B, 0x60, 0x65), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x38), -- WARNING_COLOR
            lcd.RGB(0x05, 0x16, 0x0A), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x1F, 0x24, 0x29), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-titanium.png"),
    })
end

return { init = init }
