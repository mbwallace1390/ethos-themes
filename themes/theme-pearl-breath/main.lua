-- Pearl Breath
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
        key = "PearlBr",
        name = "Pearl Breath",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x36, 0x43, 0x4B), -- SECONDARY_BGCOLOR
            lcd.RGB(0xE7, 0xEC, 0xEF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0A, 0x0D), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x73, 0x7A, 0x7F), -- DISABLE_COLOR
            lcd.RGB(0x24, 0x2D, 0x33), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xEF, 0xF2, 0xF5), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x11, 0x16, 0x1A), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x80, 0x86, 0x8B), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x66, 0x75, 0x80), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x11, 0x16, 0x1A), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-pearl-breath.png", "toolbar-pearl-breath-x18.png")),
    })
end

return { init = init }
