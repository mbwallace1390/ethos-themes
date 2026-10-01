-- Night Current
-- Standalone ETHOS radio theme with static native artwork.
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-night-current.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "NtCurr",
        name = "Night Current",
        roundButtons = true,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xE5, 0xF4, 0xF2), -- PRIMARY_COLOR
            lcd.RGB(0x19, 0x35, 0x3D), -- SECONDARY_BGCOLOR
            lcd.RGB(0x50, 0xDB, 0xC3), -- HIGHLIGHT_COLOR
            lcd.RGB(0x08, 0x14, 0x1A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6A, 0x7D, 0x80), -- DISABLE_COLOR
            lcd.RGB(0x10, 0x27, 0x2E), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xCA, 0xF0, 0xEA), -- SECONDARY_COLOR
            lcd.RGB(0x68, 0xD5, 0x94), -- SAFE_COLOR
            lcd.RGB(0x08, 0x14, 0x1A), -- PAGE_BGCOLOR
            lcd.RGB(0xF1, 0x7F, 0x8F), -- ERROR_COLOR
            lcd.RGB(0xB9, 0xEC, 0xE6), -- ACTIVE_COLOR
            lcd.RGB(0x89, 0x9C, 0x9D), -- INACTIVE_COLOR
            lcd.RGB(0xB9, 0xEC, 0xE6), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x35, 0x6A, 0x70), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xEB, 0xC3, 0x78), -- WARNING_COLOR
            lcd.RGB(0x08, 0x1A, 0x10), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x10, 0x27, 0x2E), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-night-current.png", "toolbar-night-current-x18.png"),
    })
end

return { init = init }
