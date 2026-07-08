-- Deep Space
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
local function init()
    system.registerTheme({
        key = "DSpace",
        name = "Deep Space",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF0, 0xFF), -- PRIMARY_COLOR
            lcd.RGB(0x24, 0x1B, 0x3D), -- SECONDARY_BGCOLOR
            lcd.RGB(0x9C, 0x6C, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x13, 0x0B, 0x25), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x75, 0x69, 0x8F), -- DISABLE_COLOR
            lcd.RGB(0x17, 0x11, 0x26), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xCD, 0xBC, 0xF2), -- SECONDARY_COLOR
            lcd.RGB(0x54, 0xE5, 0x9A), -- SAFE_COLOR
            lcd.RGB(0x08, 0x06, 0x0F), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x53, 0x70), -- ERROR_COLOR
            lcd.RGB(0x4E, 0xC9, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x81, 0x74, 0x9A), -- INACTIVE_COLOR
            lcd.RGB(0x4E, 0xC9, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x47, 0x37, 0x63), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD1, 0x66), -- WARNING_COLOR
            lcd.RGB(0x07, 0x1A, 0x10), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x08, 0x06, 0x0F), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-deep-space.png"),
    })
end

return { init = init }
