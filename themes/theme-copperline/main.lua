-- Copperline
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-copperline.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "CprLine",
        name = "Copperline",
        roundButtons = true,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xE9, 0xDC), -- PRIMARY_COLOR
            lcd.RGB(0x33, 0x2B, 0x24), -- SECONDARY_BGCOLOR
            lcd.RGB(0xD9, 0x93, 0x57), -- HIGHLIGHT_COLOR
            lcd.RGB(0x15, 0x11, 0x0F), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x7B, 0x74, 0x6C), -- DISABLE_COLOR
            lcd.RGB(0x23, 0x1E, 0x1A), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xEF, 0xDA, 0xC4), -- SECONDARY_COLOR
            lcd.RGB(0x68, 0xD5, 0x94), -- SAFE_COLOR
            lcd.RGB(0x15, 0x11, 0x0F), -- PAGE_BGCOLOR
            lcd.RGB(0xF1, 0x7F, 0x8F), -- ERROR_COLOR
            lcd.RGB(0xF1, 0xBD, 0x70), -- ACTIVE_COLOR
            lcd.RGB(0x99, 0x92, 0x89), -- INACTIVE_COLOR
            lcd.RGB(0xF1, 0xBD, 0x70), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x5D, 0x48, 0x38), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xEB, 0xC3, 0x78), -- WARNING_COLOR
            lcd.RGB(0x08, 0x1A, 0x10), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x23, 0x1E, 0x1A), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-copperline.png", "toolbar-copperline-x18.png"),
    })
end

return { init = init }
