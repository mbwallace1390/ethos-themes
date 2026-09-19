-- Hazard
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-hazard.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "Hazard",
        name = "Hazard",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x30, 0x2E, 0x23), -- SECONDARY_BGCOLOR
            lcd.RGB(0xFF, 0xD0, 0x00), -- HIGHLIGHT_COLOR
            lcd.RGB(0x12, 0x16, 0x1A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x77, 0x77, 0x74), -- DISABLE_COLOR
            lcd.RGB(0x1F, 0x1E, 0x18), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xFA, 0xE5, 0x87), -- SECONDARY_COLOR
            lcd.RGB(0x3F, 0xEB, 0x7F), -- SAFE_COLOR
            lcd.RGB(0x0E, 0x0E, 0x0B), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x44, 0x4D), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xD0, 0x00), -- ACTIVE_COLOR
            lcd.RGB(0x95, 0x95, 0x93), -- INACTIVE_COLOR
            lcd.RGB(0xFE, 0xD4, 0x19), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x4E, 0x4E, 0x4A), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD0, 0x00), -- WARNING_COLOR
            lcd.RGB(0x05, 0x16, 0x0A), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0E, 0x0E, 0x0B), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-hazard.png", "toolbar-hazard-x18.png"),
    })
end

return { init = init }
