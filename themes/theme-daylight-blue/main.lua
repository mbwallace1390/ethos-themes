-- Daylight Blue
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-daylight-blue.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "DayBlu",
        name = "Daylight Blue",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0x12, 0x18, 0x1E), -- PRIMARY_COLOR
            lcd.RGB(0xD5, 0xE1, 0xED), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0x6E, 0xDC), -- HIGHLIGHT_COLOR
            lcd.RGB(0xF5, 0xF7, 0xFA), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x7A, 0x80, 0x87), -- DISABLE_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x2F, 0x46, 0x5C), -- SECONDARY_COLOR
            lcd.RGB(0x14, 0x91, 0x50), -- SAFE_COLOR
            lcd.RGB(0xEC, 0xF2, 0xF9), -- PAGE_BGCOLOR
            lcd.RGB(0xCC, 0x28, 0x32), -- ERROR_COLOR
            lcd.RGB(0x00, 0x61, 0xC3), -- ACTIVE_COLOR
            lcd.RGB(0x59, 0x65, 0x6F), -- INACTIVE_COLOR
            lcd.RGB(0x00, 0x6E, 0xDC), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0xB1, 0xBD, 0xC9), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xBE, 0x73, 0x00), -- WARNING_COLOR
            lcd.RGB(0x15, 0x15, 0x16), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0xEC, 0xF2, 0xF9), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-daylight-blue.png", "toolbar-daylight-blue-x18.png"),
    })
end

return { init = init }
