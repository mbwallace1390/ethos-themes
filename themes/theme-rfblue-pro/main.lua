-- RF Blue Pro
-- Lightweight outline-focus variant of RF Suite Blue.
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
    local logoOk, toolbarLogo = pcall(lcd.loadBitmap, "logo-rfblue-pro.png")
    if not logoOk then toolbarLogo = nil end
    system.registerTheme({
        key = "RFPro",
        name = "RF Blue Pro",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            lcd.RGB(0x22, 0x2A, 0x36), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0xA8, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x12, 0x18, 0x21), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x12, 0x18, 0x21), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x08, 0x0D, 0x16), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            lcd.RGB(0x00, 0xA8, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x83, 0x91, 0xA6), -- INACTIVE_COLOR
            lcd.RGB(0x00, 0xA8, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x39, 0x46, 0x57), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x08, 0x0D, 0x16), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarLogo = toolbarLogo,
        toolbarBackground = loadToolbar("toolbar-rfblue-pro.png", "toolbar-rfblue-pro-x18.png"),
    })
end

return {
    init = init
}
