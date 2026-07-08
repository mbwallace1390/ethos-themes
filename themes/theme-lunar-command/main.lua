-- Lunar Command
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
        key = "Lunar",
        name = "Lunar Command",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF0, 0xF2, 0xF4), -- PRIMARY_COLOR
            lcd.RGB(0x41, 0x47, 0x4E), -- SECONDARY_BGCOLOR
            lcd.RGB(0xC8, 0xD0, 0xD8), -- HIGHLIGHT_COLOR
            lcd.RGB(0x1D, 0x22, 0x27), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x85, 0x8C, 0x93), -- DISABLE_COLOR
            lcd.RGB(0x2B, 0x30, 0x36), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xD2, 0xD7, 0xDC), -- SECONDARY_COLOR
            lcd.RGB(0x74, 0xD8, 0x95), -- SAFE_COLOR
            lcd.RGB(0x18, 0x1B, 0x1F), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x62), -- ERROR_COLOR
            lcd.RGB(0xE7, 0xB0, 0x4A), -- ACTIVE_COLOR
            lcd.RGB(0x92, 0x9A, 0xA2), -- INACTIVE_COLOR
            lcd.RGB(0xE7, 0xB0, 0x4A), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x60, 0x69, 0x72), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xE7, 0xB0, 0x4A), -- WARNING_COLOR
            lcd.RGB(0x0B, 0x18, 0x0F), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x18, 0x1B, 0x1F), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-lunar-command.png", "toolbar-lunar-command-x18.png")),
    })
end

return { init = init }
