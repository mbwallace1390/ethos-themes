-- Purple Hope
-- Standalone ETHOS cancer-awareness radio theme.
-- Rotorflight and RF Suite files are not modified.
local function init()
    system.registerTheme({
        key = "PurHope",
        name = "Purple Hope",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x38, 0x23, 0x4F), -- SECONDARY_BGCOLOR
            lcd.RGB(0x8D, 0x5A, 0xD8), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0A, 0x0D), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x74, 0x6C, 0x80), -- DISABLE_COLOR
            lcd.RGB(0x25, 0x17, 0x35), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xC6, 0xB0, 0xEB), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x11, 0x0B, 0x19), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xD7, 0xB8, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x81, 0x7A, 0x8C), -- INACTIVE_COLOR
            lcd.RGB(0xD7, 0xB8, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x60, 0x40, 0x80), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x11, 0x0B, 0x19), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-purple-hope.png"),
    })
end

return { init = init }
