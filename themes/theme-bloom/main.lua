-- Bloom
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
        key = "Bloom",
        name = "Bloom",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF6, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x33, 0x2B, 0x44), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x6F, 0xB5), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0C, 0x10), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x67, 0x61, 0x75), -- DISABLE_COLOR
            lcd.RGB(0x1E, 0x14, 0x30), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xF9, 0xB9, 0xDB), -- SECONDARY_COLOR
            lcd.RGB(0x48, 0xE2, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x0C, 0x08, 0x12), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x52, 0x5C), -- ERROR_COLOR
            lcd.RGB(0xA9, 0x8C, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x78, 0x73, 0x85), -- INACTIVE_COLOR
            lcd.RGB(0xB0, 0x97, 0xFE), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x4D, 0x46, 0x5C), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x06, 0x16, 0x0B), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0C, 0x08, 0x12), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-bloom.png", "toolbar-bloom-x18.png")),
    })
end

return { init = init }
