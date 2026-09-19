-- Prism
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-prism.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "Prism",
        name = "Prism",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF6, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x30, 0x2C, 0x3B), -- SECONDARY_BGCOLOR
            lcd.RGB(0xB0, 0x6C, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0C, 0x10), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x77, 0x76, 0x80), -- DISABLE_COLOR
            lcd.RGB(0x1A, 0x16, 0x26), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xD5, 0xB8, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x48, 0xE2, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x09, 0x08, 0x0E), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x52, 0x5C), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xC9, 0x4A), -- ACTIVE_COLOR
            lcd.RGB(0x95, 0x94, 0x9C), -- INACTIVE_COLOR
            lcd.RGB(0xFE, 0xCE, 0x5C), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x4A, 0x47, 0x55), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x06, 0x16, 0x0B), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x09, 0x08, 0x0E), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-prism.png", "toolbar-prism-x18.png"),
    })
end

return { init = init }
