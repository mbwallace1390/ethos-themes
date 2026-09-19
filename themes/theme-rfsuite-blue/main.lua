-- @author flyingeek
-- more widgets on my github page https://github.com/flyingeek
--
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and type(version.lcdWidth) == "number" and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function loadToolbar(largeFile, smallFile)
    -- Optional artwork must not prevent registration when it cannot be loaded.
    local ok, bitmap = pcall(lcd.loadBitmap, selectToolbar(largeFile, smallFile))
    if ok and bitmap then
        return bitmap
    end
    return nil
end

local function init()
    -- Skip unsupported firmware before creating colors or loading artwork.
    if type(system.registerTheme) ~= "function" then return end
    -- Load the optional palette-matched logo once; failures keep the theme usable.
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-rfsuite-blue.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "RFBlue",
        name = "RF Suite Blue",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF8, 0xF8, 0xF2), -- PRIMARY_COLOR
            lcd.RGB(0x42, 0x44, 0x50), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0x78, 0xE8), -- HIGHLIGHT_COLOR (blue)
            lcd.RGB(0x0C, 0x0C, 0x0C), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x82, 0x8F, 0xB6), -- DISABLE_COLOR
            lcd.RGB(0x21, 0x22, 0x2C), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xb8, 0xc3, 0xe4), -- SECONDARY_COLOR
            lcd.RGB(0x69, 0xFF, 0x94), -- SAFE_COLOR
            lcd.RGB(0x0A, 0x0F, 0x19), -- PAGE_BGCOLOR (blue-black outer gutters)
            lcd.RGB(0xDE, 0x57, 0x35), -- ERROR_COLOR
            lcd.RGB(0x76, 0xB7, 0xF3), -- ACTIVE_COLOR
            lcd.RGB(0xb8, 0xc3, 0xe4), -- INACTIVE_COLOR 0xFF, 0x80, 0xBF
            lcd.RGB(0x00, 0x78, 0xE8), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x50, 0x52, 0x61), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xA3, 0x95, 0x14), -- WARNING_COLOR
            lcd.RGB(0x0A, 0x0F, 0x19), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0A, 0x0F, 0x19), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-rfsuite-blue.png", "toolbar-rfsuite-blue-x18.png"),
    })
end
return {
    init = init
}
