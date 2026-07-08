-- @author flyingeek
-- more widgets on my github page https://github.com/flyingeek
--
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and version.lcdWidth and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function init()
    system.registerTheme({
        key = "RFBlue",
        name = "RF Suite Blue",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF8, 0xF8, 0xF2), -- PRIMARY_COLOR
            lcd.RGB(0x42, 0x44, 0x50), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0x78, 0xE8), -- HIGHLIGHT_COLOR (blue)
            lcd.RGB(0xFF, 0xFF, 0xFF), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x62, 0x72, 0xA4), -- DISABLE_COLOR
            lcd.RGB(0x21, 0x22, 0x2C), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xb8, 0xc3, 0xe4), -- SECONDARY_COLOR
            lcd.RGB(0x69, 0xFF, 0x94), -- SAFE_COLOR
            lcd.RGB(0x0A, 0x0F, 0x19), -- PAGE_BGCOLOR (blue-black outer gutters)
            lcd.RGB(0xDE, 0x57, 0x35), -- ERROR_COLOR
            lcd.RGB(0x00, 0x78, 0xE8), -- ACTIVE_COLOR
            lcd.RGB(0xb8, 0xc3, 0xe4), -- INACTIVE_COLOR 0xFF, 0x80, 0xBF
            lcd.RGB(0x00, 0x78, 0xE8), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x50, 0x52, 0x61), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xA3, 0x95, 0x14), -- WARNING_COLOR
            lcd.RGB(0x0A, 0x0F, 0x19), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0A, 0x0F, 0x19), -- TOPLCD_BGCOLOR (XE/S)
        },
        --toolbarLogo = "none",
        toolbarBackground = lcd.loadBitmap(selectToolbar("toolbar-rfsuite-blue.png", "toolbar-rfsuite-blue-x18.png")),
    })
end
return {
    init = init
}
