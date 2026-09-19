-- Carbon
-- Lightweight standalone ETHOS theme.
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-carbon.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "Carbon",
        name = "Carbon",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x22, 0x27, 0x2D), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0xB7, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x12, 0x16, 0x1A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6D, 0x70, 0x74), -- DISABLE_COLOR
            lcd.RGB(0x16, 0x1A, 0x1F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x84, 0xDA, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x3F, 0xEB, 0x7F), -- SAFE_COLOR
            lcd.RGB(0x0C, 0x0E, 0x11), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x44, 0x4D), -- ERROR_COLOR
            lcd.RGB(0x00, 0xB7, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x8A, 0x8D, 0x90), -- INACTIVE_COLOR
            lcd.RGB(0x18, 0xBD, 0xFE), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x47, 0x4B, 0x4F), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x38), -- WARNING_COLOR
            lcd.RGB(0x05, 0x16, 0x0A), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0C, 0x0E, 0x11), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-carbon.png", "toolbar-carbon-x18.png"),
    })
end

return { init = init }
