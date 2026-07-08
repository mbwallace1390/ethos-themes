-- Neon Fusion
-- Lightweight standalone ETHOS theme.
local function init()
    system.registerTheme({
        key = "NeoFus",
        name = "Neon Fusion",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x1A, 0x2B, 0x2E), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0xD7, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x09, 0x13, 0x14), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x5E, 0x66, 0x69), -- DISABLE_COLOR
            lcd.RGB(0x10, 0x1C, 0x1F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x7F, 0xE8, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x4E, 0xEF, 0x84), -- SAFE_COLOR
            lcd.RGB(0x08, 0x0F, 0x11), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x48, 0x4D), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x3E, 0xA5), -- ACTIVE_COLOR
            lcd.RGB(0x6C, 0x74, 0x77), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0x3E, 0xA5), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x45, 0x4E, 0x51), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x44), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x08, 0x0F, 0x11), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-neon-fusion.png"),
    })
end

return { init = init }
