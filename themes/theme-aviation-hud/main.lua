-- Aviation HUD
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
local function init()
    system.registerTheme({
        key = "AvHUD",
        name = "Aviation HUD",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xD9, 0xFF, 0xE2), -- PRIMARY_COLOR
            lcd.RGB(0x12, 0x27, 0x1A), -- SECONDARY_BGCOLOR
            lcd.RGB(0x62, 0xFF, 0x86), -- HIGHLIGHT_COLOR
            lcd.RGB(0x06, 0x14, 0x0A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x55, 0x72, 0x5C), -- DISABLE_COLOR
            lcd.RGB(0x0B, 0x1B, 0x11), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x9A, 0xEF, 0xAC), -- SECONDARY_COLOR
            lcd.RGB(0x62, 0xFF, 0x86), -- SAFE_COLOR
            lcd.RGB(0x05, 0x0D, 0x08), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4B, 0x4B), -- ERROR_COLOR
            lcd.RGB(0xB8, 0xFF, 0x4A), -- ACTIVE_COLOR
            lcd.RGB(0x68, 0x8A, 0x70), -- INACTIVE_COLOR
            lcd.RGB(0xB8, 0xFF, 0x4A), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x29, 0x4E, 0x33), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD2, 0x4A), -- WARNING_COLOR
            lcd.RGB(0x03, 0x10, 0x06), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x05, 0x0D, 0x08), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-aviation-hud.png"),
    })
end

return { init = init }
