-- Soft Mint
-- Lightweight standalone ETHOS theme.
local function init()
    system.registerTheme({
        key = "SMint",
        name = "Soft Mint",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x34, 0x45, 0x3E), -- SECONDARY_BGCOLOR
            lcd.RGB(0x91, 0xE7, 0xC1), -- HIGHLIGHT_COLOR
            lcd.RGB(0x1B, 0x29, 0x22), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x75, 0x7D, 0x7B), -- DISABLE_COLOR
            lcd.RGB(0x26, 0x33, 0x2D), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xC3, 0xEF, 0xDE), -- SECONDARY_COLOR
            lcd.RGB(0x8C, 0xE7, 0xB4), -- SAFE_COLOR
            lcd.RGB(0x1A, 0x24, 0x1F), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x75, 0x80), -- ERROR_COLOR
            lcd.RGB(0x91, 0xE7, 0xC1), -- ACTIVE_COLOR
            lcd.RGB(0x85, 0x8D, 0x8B), -- INACTIVE_COLOR
            lcd.RGB(0xA5, 0xEA, 0xCC), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x5E, 0x68, 0x64), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD0, 0x75), -- WARNING_COLOR
            lcd.RGB(0x14, 0x2A, 0x1E), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x1A, 0x24, 0x1F), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap("toolbar-soft-mint.png"),
    })
end

return { init = init }
