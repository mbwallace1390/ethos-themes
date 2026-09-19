-- Desert Tactical
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-desert-tactical.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "DesTac",
        name = "Desert Tactical",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0x2E, 0x24, 0x18), -- PRIMARY_COLOR
            lcd.RGB(0xC9, 0xB3, 0x8C), -- SECONDARY_BGCOLOR
            lcd.RGB(0xA8, 0x5C, 0x24), -- HIGHLIGHT_COLOR
            lcd.RGB(0xFF, 0xF8, 0xEA), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6D, 0x60, 0x4E), -- DISABLE_COLOR
            lcd.RGB(0xE3, 0xD2, 0xB1), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x59, 0x44, 0x2E), -- SECONDARY_COLOR
            lcd.RGB(0x3B, 0x84, 0x58), -- SAFE_COLOR
            lcd.RGB(0xF1, 0xE7, 0xD2), -- PAGE_BGCOLOR
            lcd.RGB(0xB8, 0x38, 0x32), -- ERROR_COLOR
            lcd.RGB(0x70, 0x39, 0x15), -- ACTIVE_COLOR
            lcd.RGB(0x53, 0x45, 0x34), -- INACTIVE_COLOR
            lcd.RGB(0x7B, 0x3E, 0x17), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0xB2, 0x9B, 0x74), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xA1, 0x5E, 0x00), -- WARNING_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0xF1, 0xE7, 0xD2), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-desert-tactical.png", "toolbar-desert-tactical-x18.png"),
    })
end

return { init = init }
