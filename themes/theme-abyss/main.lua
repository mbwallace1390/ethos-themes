-- Abyss
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-abyss.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "Abyss",
        name = "Abyss",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF6, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x23, 0x2E, 0x3B), -- SECONDARY_BGCOLOR
            lcd.RGB(0x2B, 0xC8, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0C, 0x0C, 0x10), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6F, 0x76, 0x80), -- DISABLE_COLOR
            lcd.RGB(0x0C, 0x18, 0x26), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x9A, 0xE1, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x48, 0xE2, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x04, 0x09, 0x0E), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x52, 0x5C), -- ERROR_COLOR
            lcd.RGB(0x7F, 0xE9, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x8E, 0x94, 0x9C), -- INACTIVE_COLOR
            lcd.RGB(0x8B, 0xEA, 0xFE), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x3F, 0x49, 0x55), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x06, 0x16, 0x0B), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x04, 0x09, 0x0E), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-abyss.png", "toolbar-abyss-x18.png"),
    })
end

return { init = init }
