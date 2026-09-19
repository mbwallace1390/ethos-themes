-- Daylight Green
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-daylight-green.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "DayGrn",
        name = "Daylight Green",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0x12, 0x18, 0x1E), -- PRIMARY_COLOR
            lcd.RGB(0xD7, 0xE3, 0xE1), -- SECONDARY_BGCOLOR
            lcd.RGB(0x13, 0x8A, 0x4B), -- HIGHLIGHT_COLOR
            lcd.RGB(0x09, 0x09, 0x0A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x7A, 0x81, 0x87), -- DISABLE_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x31, 0x48, 0x4E), -- SECONDARY_COLOR
            lcd.RGB(0x14, 0x91, 0x50), -- SAFE_COLOR
            lcd.RGB(0xED, 0xF3, 0xF4), -- PAGE_BGCOLOR
            lcd.RGB(0xCC, 0x28, 0x32), -- ERROR_COLOR
            lcd.RGB(0x10, 0x73, 0x3F), -- ACTIVE_COLOR
            lcd.RGB(0x5A, 0x65, 0x71), -- INACTIVE_COLOR
            lcd.RGB(0x13, 0x8A, 0x4B), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0xB2, 0xBF, 0xC0), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xBE, 0x73, 0x00), -- WARNING_COLOR
            lcd.RGB(0x15, 0x15, 0x16), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0xED, 0xF3, 0xF4), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-daylight-green.png", "toolbar-daylight-green-x18.png"),
    })
end

return { init = init }
