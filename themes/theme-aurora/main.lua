-- Aurora
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
        key = "Aurora",
        name = "Aurora",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF6, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x28, 0x32, 0x41), -- SECONDARY_BGCOLOR
            lcd.RGB(0x4B, 0xE3, 0x8B), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0C, 0x10), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x5E, 0x66, 0x72), -- DISABLE_COLOR
            lcd.RGB(0x11, 0x1C, 0x2C), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xA8, 0xED, 0xC8), -- SECONDARY_COLOR
            lcd.RGB(0x48, 0xE2, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x06, 0x0A, 0x10), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x52, 0x5C), -- ERROR_COLOR
            lcd.RGB(0xA6, 0x6C, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x70, 0x78, 0x83), -- INACTIVE_COLOR
            lcd.RGB(0xAE, 0x7A, 0xFE), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x43, 0x4C, 0x59), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x06, 0x16, 0x0B), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x06, 0x0A, 0x10), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-aurora.png", "toolbar-aurora-x18.png")),
    })
end

return { init = init }
