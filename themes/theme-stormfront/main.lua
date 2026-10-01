-- Stormfront
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-stormfront.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "Stormfr",
        name = "Stormfront",
        roundButtons = true,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xEA, 0xF4, 0xFF), -- PRIMARY_COLOR
            lcd.RGB(0x23, 0x3B, 0x4B), -- SECONDARY_BGCOLOR
            lcd.RGB(0x61, 0xBA, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x08, 0x15, 0x1F), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x73, 0x84, 0x91), -- DISABLE_COLOR
            lcd.RGB(0x14, 0x2A, 0x3A), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xD1, 0xEA, 0xFF), -- SECONDARY_COLOR
            lcd.RGB(0x68, 0xD5, 0x94), -- SAFE_COLOR
            lcd.RGB(0x08, 0x15, 0x1F), -- PAGE_BGCOLOR
            lcd.RGB(0xF1, 0x7F, 0x8F), -- ERROR_COLOR
            lcd.RGB(0xB9, 0xE3, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x95, 0xA3, 0xAE), -- INACTIVE_COLOR
            lcd.RGB(0xB9, 0xE3, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x35, 0x5D, 0x72), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xEB, 0xC3, 0x78), -- WARNING_COLOR
            lcd.RGB(0x08, 0x1A, 0x10), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x14, 0x2A, 0x3A), -- TOPLCD_BGCOLOR
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-stormfront.png", "toolbar-stormfront-x18.png"),
    })
end

return { init = init }
