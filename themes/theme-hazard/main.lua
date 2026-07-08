-- Hazard
-- Lightweight standalone ETHOS theme.
local function init()
    system.registerTheme({
        key = "Hazard",
        name = "Hazard",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x30, 0x2E, 0x23), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0xD0, 0x00), -- HIGHLIGHT_COLOR
            lcd.RGB(0x12, 0x16, 0x1A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6A, 0x6A, 0x67), -- DISABLE_COLOR
            lcd.RGB(0x1F, 0x1E, 0x18), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xFA, 0xE5, 0x87), -- SECONDARY_COLOR
            lcd.RGB(0x3F, 0xEB, 0x7F), -- SAFE_COLOR
            lcd.RGB(0x0E, 0x0E, 0x0B), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x44, 0x4D), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xD0, 0x00), -- ACTIVE_COLOR
            lcd.RGB(0x7B, 0x7B, 0x79), -- INACTIVE_COLOR
            lcd.RGB(0xFE, 0xD4, 0x19), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x4E, 0x4E, 0x4A), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD0, 0x00), -- WARNING_COLOR
            lcd.RGB(0x05, 0x16, 0x0A), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0E, 0x0E, 0x0B), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-hazard.png"),
    })
end

return { init = init }
