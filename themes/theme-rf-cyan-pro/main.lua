-- RF Cyan Pro
-- Lightweight RF Pro outline-focus color variant.
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
    system.registerTheme({
        key = "RFCyan",
        name = "RF Cyan Pro",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            lcd.RGB(0x14, 0x2B, 0x34), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0xD4, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0A, 0x1B, 0x22), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x0A, 0x1B, 0x22), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x05, 0x0F, 0x14), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            lcd.RGB(0x00, 0xD4, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x66, 0x96, 0xA3), -- INACTIVE_COLOR
            lcd.RGB(0x00, 0xD4, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x27, 0x4F, 0x5E), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x05, 0x0F, 0x14), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarBackground = loadToolbar("toolbar-rf-cyan-pro.png", "toolbar-rf-cyan-pro-x18.png"),
    })
end

return {
    init = init
}
