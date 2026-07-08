-- Midnight Blueprint
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
local function init()
    system.registerTheme({
        key = "MidBpt",
        name = "Midnight Blueprint",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xE7, 0xF6, 0xFF), -- PRIMARY_COLOR
            lcd.RGB(0x14, 0x36, 0x51), -- SECONDARY_BGCOLOR
            lcd.RGB(0x62, 0xC8, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x07, 0x18, 0x26), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6A, 0x87, 0x9B), -- DISABLE_COLOR
            lcd.RGB(0x0D, 0x26, 0x3B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xB5, 0xE1, 0xF8), -- SECONDARY_COLOR
            lcd.RGB(0x58, 0xE6, 0x9A), -- SAFE_COLOR
            lcd.RGB(0x07, 0x17, 0x25), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5B, 0x68), -- ERROR_COLOR
            lcd.RGB(0xF4, 0xF7, 0xFA), -- ACTIVE_COLOR
            lcd.RGB(0x78, 0x98, 0xAD), -- INACTIVE_COLOR
            lcd.RGB(0xF4, 0xF7, 0xFA), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x34, 0x5C, 0x77), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD0, 0x6A), -- WARNING_COLOR
            lcd.RGB(0x07, 0x1A, 0x10), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x07, 0x17, 0x25), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-midnight-blueprint.png"),
    })
end

return { init = init }
