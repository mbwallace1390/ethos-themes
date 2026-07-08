-- Green Courage
-- Standalone ETHOS cancer-awareness radio theme.
-- Rotorflight and RF Suite files are not modified.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and version.lcdWidth and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function init()
    system.registerTheme({
        key = "GrnCour",
        name = "Green Courage",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x19, 0x41, 0x26), -- SECONDARY_BGCOLOR
            lcd.RGB(0x36, 0xB9, 0x6B), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x67, 0x79, 0x6E), -- DISABLE_COLOR
            lcd.RGB(0x10, 0x2B, 0x19), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x9F, 0xDB, 0xBA), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x07, 0x15, 0x0C), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xA8, 0xF0, 0xC0), -- ACTIVE_COLOR
            lcd.RGB(0x75, 0x85, 0x7C), -- INACTIVE_COLOR
            lcd.RGB(0xA8, 0xF0, 0xC0), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x2D, 0x70, 0x44), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x07, 0x15, 0x0C), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-green-courage.png", "toolbar-green-courage-x18.png")),
    })
end

return { init = init }
