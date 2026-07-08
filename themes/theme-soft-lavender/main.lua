-- Soft Lavender
-- Lightweight standalone ETHOS theme.
local function init()
    system.registerTheme({
        key = "SoftLav",
        name = "Soft Lavender",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x39, 0x34, 0x45), -- SECONDARY_BGCOLOR
            lcd.RGB(0xB7, 0x9C, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x1E, 0x1B, 0x29), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x77, 0x75, 0x7F), -- DISABLE_COLOR
            lcd.RGB(0x2A, 0x26, 0x33), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xD6, 0xCA, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x8C, 0xE7, 0xB4), -- SAFE_COLOR
            lcd.RGB(0x1C, 0x1A, 0x24), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x75, 0x80), -- ERROR_COLOR
            lcd.RGB(0xB7, 0x9C, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x87, 0x86, 0x8F), -- INACTIVE_COLOR
            lcd.RGB(0xC3, 0xAE, 0xFE), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x61, 0x5E, 0x69), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD0, 0x75), -- WARNING_COLOR
            lcd.RGB(0x14, 0x2A, 0x1E), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x1C, 0x1A, 0x24), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-soft-lavender.png"),
    })
end

return { init = init }
