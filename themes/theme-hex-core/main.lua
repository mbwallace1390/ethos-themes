-- Hex Core
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
        key = "HexCore",
        name = "Hex Core",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF3, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x26, 0x31, 0x3D), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0x8A, 0x3D), -- HIGHLIGHT_COLOR
            lcd.RGB(0x23, 0x10, 0x06), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x72, 0x80, 0x8C), -- DISABLE_COLOR
            lcd.RGB(0x18, 0x22, 0x2C), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xC0, 0xCD, 0xD7), -- SECONDARY_COLOR
            lcd.RGB(0x54, 0xDF, 0x91), -- SAFE_COLOR
            lcd.RGB(0x0B, 0x11, 0x17), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4F, 0x5E), -- ERROR_COLOR
            lcd.RGB(0x44, 0xC7, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x82, 0x91, 0x9D), -- INACTIVE_COLOR
            lcd.RGB(0x44, 0xC7, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x3C, 0x4E, 0x5D), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC1, 0x4A), -- WARNING_COLOR
            lcd.RGB(0x07, 0x19, 0x0E), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0B, 0x11, 0x17), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-hex-core.png", "toolbar-hex-core-x18.png")),
    })
end

return { init = init }
