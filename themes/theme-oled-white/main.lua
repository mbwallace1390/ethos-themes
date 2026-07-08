-- OLED White
-- Lightweight standalone ETHOS theme.
local function init()
    system.registerTheme({
        key = "OLWht",
        name = "OLED White",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x15, 0x15, 0x16), -- SECONDARY_BGCOLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- HIGHLIGHT_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x48, 0x4E, 0x56), -- DISABLE_COLOR
            lcd.RGB(0x0B, 0x0B, 0x0B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- SECONDARY_COLOR
            lcd.RGB(0x3C, 0xFF, 0x7A), -- SAFE_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x40, 0x4F), -- ERROR_COLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- ACTIVE_COLOR
            lcd.RGB(0x64, 0x65, 0x66), -- INACTIVE_COLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x3A, 0x3A, 0x3B), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC4, 0x37), -- WARNING_COLOR
            lcd.RGB(0x00, 0x12, 0x05), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x00, 0x00, 0x00), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-oled-white.png"),
    })
end

return { init = init }
