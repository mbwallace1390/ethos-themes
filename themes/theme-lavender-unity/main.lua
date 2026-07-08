-- Lavender Unity
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
        key = "LavUnt",
        name = "Lavender Unity",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x3C, 0x30, 0x55), -- SECONDARY_BGCOLOR
            lcd.RGB(0xB7, 0x9C, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0A, 0x0D), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x77, 0x72, 0x84), -- DISABLE_COLOR
            lcd.RGB(0x29, 0x20, 0x3B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xD9, 0xCE, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x14, 0x10, 0x1D), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xE2, 0xD7, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x83, 0x7F, 0x8F), -- INACTIVE_COLOR
            lcd.RGB(0xE2, 0xD7, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x66, 0x52, 0x85), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x14, 0x10, 0x1D), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-lavender-unity.png", "toolbar-lavender-unity-x18.png")),
    })
end

return { init = init }
