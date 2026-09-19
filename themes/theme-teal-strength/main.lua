-- Teal Strength
-- Standalone ETHOS cancer-awareness radio theme.
-- Rotorflight and RF Suite files are not modified.
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-teal-strength.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "TealStr",
        name = "Teal Strength",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x19, 0x49, 0x43), -- SECONDARY_BGCOLOR
            lcd.RGB(0x22, 0xC7, 0xB8), -- HIGHLIGHT_COLOR
            lcd.RGB(0x10, 0x30, 0x2D), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x7E, 0x90, 0x8F), -- DISABLE_COLOR
            lcd.RGB(0x10, 0x30, 0x2D), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x96, 0xE1, 0xDC), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x07, 0x18, 0x17), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0x8E, 0xF3, 0xE9), -- ACTIVE_COLOR
            lcd.RGB(0xA3, 0xB0, 0xAF), -- INACTIVE_COLOR
            lcd.RGB(0x8E, 0xF3, 0xE9), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x2C, 0x74, 0x6B), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x07, 0x18, 0x17), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-teal-strength.png", "toolbar-teal-strength-x18.png"),
    })
end

return { init = init }
