/**
 * Who runs the site, for the Impressum (§ 5 DDG). A row with an empty value
 * is not shown; a German Impressum needs a postal address and a way to reach
 * the operator quickly, so fill both in before publishing.
 */
export const OPERATOR = {
  name: 'Julius Sommer',
  /** Postal address, one line per entry. */
  address: [] as string[],
  email: '',
};
