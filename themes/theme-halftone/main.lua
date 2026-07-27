-- Halftone
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
        key = "Halftn",
        name = "Halftone",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF6, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x32, 0x32, 0x35), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x4D, 0x5E), -- HIGHLIGHT_COLOR
            lcd.RGB(0xF4, 0xF6, 0xFA), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x65, 0x66, 0x69), -- DISABLE_COLOR
            lcd.RGB(0x1C, 0x1C, 0x1F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xF9, 0xAA, 0xB4), -- SECONDARY_COLOR
            lcd.RGB(0x48, 0xE2, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x0B, 0x0B, 0x0C), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x52, 0x5C), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xB0, 0x20), -- ACTIVE_COLOR
            lcd.RGB(0x77, 0x78, 0x7B), -- INACTIVE_COLOR
            lcd.RGB(0xFE, 0xB7, 0x36), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x4C, 0x4C, 0x4F), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x06, 0x16, 0x0B), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0B, 0x0B, 0x0C), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-halftone.png", "toolbar-halftone-x18.png")),
    })
end

return { init = init }
