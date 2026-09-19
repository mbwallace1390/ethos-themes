-- Purple Hope
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-purple-hope.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "PurHope",
        name = "Purple Hope",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x38, 0x23, 0x4F), -- SECONDARY_BGCOLOR
            lcd.RGB(0x8D, 0x5A, 0xD8), -- HIGHLIGHT_COLOR
            lcd.RGB(0x03, 0x03, 0x04), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x7A, 0x72, 0x85), -- DISABLE_COLOR
            lcd.RGB(0x25, 0x17, 0x35), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xC6, 0xB0, 0xEB), -- SECONDARY_COLOR
            lcd.RGB(0x56, 0xE2, 0x89), -- SAFE_COLOR
            lcd.RGB(0x11, 0x0B, 0x19), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x4E, 0x58), -- ERROR_COLOR
            lcd.RGB(0xD7, 0xB8, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x96, 0x91, 0x9F), -- INACTIVE_COLOR
            lcd.RGB(0xD7, 0xB8, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x60, 0x40, 0x80), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x48), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x11, 0x0B, 0x19), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-purple-hope.png", "toolbar-purple-hope-x18.png"),
    })
end

return { init = init }
