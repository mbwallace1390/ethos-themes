-- Circuit Trace
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and version.lcdWidth and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function init()
    system.registerTheme({
        key = "CirTrce",
        name = "Circuit Trace",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xE7, 0xF9, 0xE8), -- PRIMARY_COLOR
            lcd.RGB(0x17, 0x3B, 0x2A), -- SECONDARY_BGCOLOR
            lcd.RGB(0x44, 0xE5, 0x7A), -- HIGHLIGHT_COLOR
            lcd.RGB(0x06, 0x18, 0x0C), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x5F, 0x80, 0x6A), -- DISABLE_COLOR
            lcd.RGB(0x0D, 0x28, 0x1B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xA9, 0xDF, 0xB7), -- SECONDARY_COLOR
            lcd.RGB(0x44, 0xE5, 0x7A), -- SAFE_COLOR
            lcd.RGB(0x06, 0x15, 0x0E), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x53, 0x60), -- ERROR_COLOR
            lcd.RGB(0xF0, 0xD8, 0x4D), -- ACTIVE_COLOR
            lcd.RGB(0x6D, 0x92, 0x78), -- INACTIVE_COLOR
            lcd.RGB(0xF0, 0xD8, 0x4D), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x2C, 0x5A, 0x3E), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xF0, 0xD8, 0x4D), -- WARNING_COLOR
            lcd.RGB(0x06, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x06, 0x15, 0x0E), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-circuit-trace.png", "toolbar-circuit-trace-x18.png")),
    })
end

return { init = init }
