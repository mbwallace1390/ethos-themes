-- Rotor Command
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
        key = "RotorCm",
        name = "Rotor Command",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xEA, 0xF7, 0xF7), -- PRIMARY_COLOR
            lcd.RGB(0x17, 0x36, 0x38), -- SECONDARY_BGCOLOR
            lcd.RGB(0x37, 0xD4, 0xC9), -- HIGHLIGHT_COLOR
            lcd.RGB(0x06, 0x1A, 0x1A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x66, 0x88, 0x89), -- DISABLE_COLOR
            lcd.RGB(0x0D, 0x24, 0x26), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xA9, 0xDE, 0xDC), -- SECONDARY_COLOR
            lcd.RGB(0x65, 0xE6, 0x8D), -- SAFE_COLOR
            lcd.RGB(0x06, 0x15, 0x16), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x50, 0x58), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x66, 0x4D), -- ACTIVE_COLOR
            lcd.RGB(0x71, 0x97, 0x98), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0x66, 0x4D), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x31, 0x5C, 0x5E), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD1, 0x66), -- WARNING_COLOR
            lcd.RGB(0x07, 0x1A, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x06, 0x15, 0x16), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-rotor-command.png", "toolbar-rotor-command-x18.png")),
    })
end

return { init = init }
