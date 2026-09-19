-- Arctic Tactical
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-arctic-tactical.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "ArcTac",
        name = "Arctic Tactical",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0x17, 0x24, 0x2E), -- PRIMARY_COLOR
            lcd.RGB(0xCA, 0xD6, 0xDC), -- SECONDARY_BGCOLOR
            lcd.RGB(0x16, 0x79, 0xA8), -- HIGHLIGHT_COLOR
            lcd.RGB(0xF6, 0xFB, 0xFE), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6B, 0x79, 0x82), -- DISABLE_COLOR
            lcd.RGB(0xE6, 0xED, 0xF0), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x3E, 0x5D, 0x70), -- SECONDARY_COLOR
            lcd.RGB(0x16, 0x8A, 0x59), -- SAFE_COLOR
            lcd.RGB(0xF5, 0xF8, 0xFA), -- PAGE_BGCOLOR
            lcd.RGB(0xC9, 0x36, 0x45), -- ERROR_COLOR
            lcd.RGB(0x0C, 0x5D, 0x86), -- ACTIVE_COLOR
            lcd.RGB(0x51, 0x5E, 0x66), -- INACTIVE_COLOR
            lcd.RGB(0x0C, 0x5D, 0x86), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0xAA, 0xBB, 0xC4), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xA7, 0x64, 0x00), -- WARNING_COLOR
            lcd.RGB(0x0B, 0x0B, 0x0B), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0xF5, 0xF8, 0xFA), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-arctic-tactical.png", "toolbar-arctic-tactical-x18.png"),
    })
end

return { init = init }
