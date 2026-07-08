-- Neon Horizon
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
local function init()
    system.registerTheme({
        key = "NeoHor",
        name = "Neon Horizon",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF7, 0xF1, 0xFF), -- PRIMARY_COLOR
            lcd.RGB(0x2B, 0x1B, 0x49), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x4F, 0xB8), -- HIGHLIGHT_COLOR
            lcd.RGB(0x25, 0x0A, 0x20), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x80, 0x6A, 0x92), -- DISABLE_COLOR
            lcd.RGB(0x1A, 0x12, 0x30), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xD9, 0xBA, 0xF4), -- SECONDARY_COLOR
            lcd.RGB(0x5F, 0xE8, 0xA5), -- SAFE_COLOR
            lcd.RGB(0x0B, 0x07, 0x16), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4D, 0x6D), -- ERROR_COLOR
            lcd.RGB(0x34, 0xD8, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x8B, 0x73, 0xA0), -- INACTIVE_COLOR
            lcd.RGB(0x34, 0xD8, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x58, 0x36, 0x6F), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD1, 0x66), -- WARNING_COLOR
            lcd.RGB(0x07, 0x1A, 0x11), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0B, 0x07, 0x16), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-neon-horizon.png"),
    })
end

return { init = init }
